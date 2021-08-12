package kr.ac.kpu.firstproject.ui.main

import android.content.Context
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentPagerAdapter
import kr.ac.kpu.firstproject.R

private val MainTextArray = arrayOf(
    R.string.WalkThroughMainText1,
    R.string.WalkThroughMainText2,
    R.string.WalkThroughMainText3,
    R.string.WalkThroughMainText4
)

private val SubTextArray = arrayOf(
    R.string.WalkThroughSubText1,
    R.string.WalkThroughSubText2,
    R.string.WalkThroughSubText3,
    R.string.WalkThroughSubText4
)

class SectionsPagerAdapter(private val context: Context, fm: FragmentManager) : FragmentPagerAdapter(fm, BEHAVIOR_RESUME_ONLY_CURRENT_FRAGMENT) {

    override fun getItem(position: Int): Fragment {
        /*
        index, MainText, SubText를 넣어 Fragment를 생성 후 반환
         */
        return PlaceholderFragment.newInstance(position, context.resources.getString( //PlaceHolder에 그때의 position을 받아서 어떤 페이지 형식을 만들지 정의
            MainTextArray[position]), context.resources.getString(SubTextArray[position]))
    }

    override fun getCount(): Int {
        return 4
    }
}